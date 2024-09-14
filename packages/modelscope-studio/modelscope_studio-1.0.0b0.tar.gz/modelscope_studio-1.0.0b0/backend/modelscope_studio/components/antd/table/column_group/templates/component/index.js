function X(e) {
  const {
    gradio: t,
    _internal: i,
    ...n
  } = e;
  return Object.keys(i).reduce((o, s) => {
    const l = s.match(/bind_(.+)_event/);
    if (l) {
      const c = l[1], u = c.split("_"), _ = (...m) => {
        const b = m.map((f) => m && typeof f == "object" && (f.nativeEvent || f instanceof Event) ? {
          type: f.type,
          detail: f.detail,
          timestamp: f.timeStamp,
          clientX: f.clientX,
          clientY: f.clientY,
          targetId: f.target.id,
          targetClassName: f.target.className,
          altKey: f.altKey,
          ctrlKey: f.ctrlKey,
          shiftKey: f.shiftKey,
          metaKey: f.metaKey
        } : f);
        return t.dispatch(c.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: b,
          component: n
        });
      };
      if (u.length > 1) {
        let m = {
          ...n.props[u[0]] || {}
        };
        o[u[0]] = m;
        for (let f = 1; f < u.length - 1; f++) {
          const h = {
            ...n.props[u[f]] || {}
          };
          m[u[f]] = h, m = h;
        }
        const b = u[u.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = _, o;
      }
      const a = u[0];
      o[`on${a.slice(0, 1).toUpperCase()}${a.slice(1)}`] = _;
    }
    return o;
  }, {});
}
function k() {
}
function Y(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function D(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return k;
  }
  const i = e.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function g(e) {
  let t;
  return D(e, (i) => t = i)(), t;
}
const p = [];
function y(e, t = k) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function o(c) {
    if (Y(e, c) && (e = c, i)) {
      const u = !p.length;
      for (const _ of n)
        _[1](), p.push(_, e);
      if (u) {
        for (let _ = 0; _ < p.length; _ += 2)
          p[_][0](p[_ + 1]);
        p.length = 0;
      }
    }
  }
  function s(c) {
    o(c(e));
  }
  function l(c, u = k) {
    const _ = [c, u];
    return n.add(_), n.size === 1 && (i = t(o, s) || k), c(e), () => {
      n.delete(_), n.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: s,
    subscribe: l
  };
}
const {
  getContext: A,
  setContext: P
} = window.__gradio__svelte__internal, L = "$$ms-gr-antd-slots-key";
function Z() {
  const e = y({});
  return P(L, e);
}
const B = "$$ms-gr-antd-context-key";
function G(e) {
  var c;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = V(), i = Q({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((u) => {
    i.slotKey.set(u);
  }), H();
  const n = A(B), o = ((c = g(n)) == null ? void 0 : c.as_item) || e.as_item, s = n ? o ? g(n)[o] : g(n) : {}, l = y({
    ...e,
    ...s
  });
  return n ? (n.subscribe((u) => {
    const {
      as_item: _
    } = g(l);
    _ && (u = u[_]), l.update((a) => ({
      ...a,
      ...u
    }));
  }), [l, (u) => {
    const _ = u.as_item ? g(n)[u.as_item] : g(n);
    return l.set({
      ...u,
      ..._
    });
  }]) : [l, (u) => {
    l.set(u);
  }];
}
const M = "$$ms-gr-antd-slot-key";
function H() {
  P(M, y(void 0));
}
function V() {
  return A(M);
}
const J = "$$ms-gr-antd-component-slot-context-key";
function Q({
  slot: e,
  index: t,
  subIndex: i
}) {
  return P(J, {
    slotKey: y(e),
    slotIndex: y(t),
    subSlotIndex: y(i)
  });
}
function T(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var z = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function i() {
      for (var s = "", l = 0; l < arguments.length; l++) {
        var c = arguments[l];
        c && (s = o(s, n(c)));
      }
      return s;
    }
    function n(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return i.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var l = "";
      for (var c in s)
        t.call(s, c) && s[c] && (l = o(l, c));
      return l;
    }
    function o(s, l) {
      return l ? s ? s + " " + l : s + l : s;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(z);
var W = z.exports;
const $ = /* @__PURE__ */ T(W), {
  getContext: tt,
  setContext: et
} = window.__gradio__svelte__internal;
function nt(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function i(o = ["default"]) {
    const s = o.reduce((l, c) => (l[c] = y([]), l), {});
    return et(t, {
      itemsMap: s,
      allowedSlots: o
    }), s;
  }
  function n() {
    const {
      itemsMap: o,
      allowedSlots: s
    } = tt(t);
    return function(l, c, u) {
      o && (l ? o[l].update((_) => {
        const a = [..._];
        return s.includes(l) ? a[c] = u : a[c] = void 0, a;
      }) : s.includes("default") && o.default.update((_) => {
        const a = [..._];
        return a[c] = u, a;
      }));
    };
  }
  return {
    getItems: i,
    getSetItemFn: n
  };
}
const {
  getItems: st,
  getSetItemFn: it
} = nt("table-column"), {
  SvelteComponent: ot,
  check_outros: lt,
  component_subscribe: x,
  create_slot: rt,
  detach: ct,
  empty: ut,
  flush: d,
  get_all_dirty_from_scope: ft,
  get_slot_changes: _t,
  group_outros: at,
  init: mt,
  insert: dt,
  safe_not_equal: bt,
  transition_in: v,
  transition_out: j,
  update_slot_base: yt
} = window.__gradio__svelte__internal;
function F(e) {
  let t;
  const i = (
    /*#slots*/
    e[20].default
  ), n = rt(
    i,
    e,
    /*$$scope*/
    e[19],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(o, s) {
      n && n.m(o, s), t = !0;
    },
    p(o, s) {
      n && n.p && (!t || s & /*$$scope*/
      524288) && yt(
        n,
        i,
        o,
        /*$$scope*/
        o[19],
        t ? _t(
          i,
          /*$$scope*/
          o[19],
          s,
          null
        ) : ft(
          /*$$scope*/
          o[19]
        ),
        null
      );
    },
    i(o) {
      t || (v(n, o), t = !0);
    },
    o(o) {
      j(n, o), t = !1;
    },
    d(o) {
      n && n.d(o);
    }
  };
}
function ht(e) {
  let t, i, n = (
    /*$mergedProps*/
    e[0].visible && F(e)
  );
  return {
    c() {
      n && n.c(), t = ut();
    },
    m(o, s) {
      n && n.m(o, s), dt(o, t, s), i = !0;
    },
    p(o, [s]) {
      /*$mergedProps*/
      o[0].visible ? n ? (n.p(o, s), s & /*$mergedProps*/
      1 && v(n, 1)) : (n = F(o), n.c(), v(n, 1), n.m(t.parentNode, t)) : n && (at(), j(n, 1, 1, () => {
        n = null;
      }), lt());
    },
    i(o) {
      i || (v(n), i = !0);
    },
    o(o) {
      j(n), i = !1;
    },
    d(o) {
      o && ct(t), n && n.d(o);
    }
  };
}
function gt(e, t, i) {
  let n, o, s, l, c, {
    $$slots: u = {},
    $$scope: _
  } = t, {
    gradio: a
  } = t, {
    props: m = {}
  } = t;
  const b = y(m);
  x(e, b, (r) => i(18, c = r));
  let {
    _internal: f = {}
  } = t, {
    title: h
  } = t, {
    as_item: C
  } = t, {
    visible: S = !0
  } = t, {
    elem_id: K = ""
  } = t, {
    elem_classes: I = []
  } = t, {
    elem_style: w = {}
  } = t;
  const E = V();
  x(e, E, (r) => i(17, l = r));
  const [N, R] = G({
    gradio: a,
    props: c,
    _internal: f,
    visible: S,
    elem_id: K,
    elem_classes: I,
    elem_style: w,
    as_item: C,
    title: h
  });
  x(e, N, (r) => i(0, s = r));
  const O = Z();
  x(e, O, (r) => i(16, o = r));
  const U = it(), {
    default: q
  } = st();
  return x(e, q, (r) => i(15, n = r)), e.$$set = (r) => {
    "gradio" in r && i(6, a = r.gradio), "props" in r && i(7, m = r.props), "_internal" in r && i(8, f = r._internal), "title" in r && i(9, h = r.title), "as_item" in r && i(10, C = r.as_item), "visible" in r && i(11, S = r.visible), "elem_id" in r && i(12, K = r.elem_id), "elem_classes" in r && i(13, I = r.elem_classes), "elem_style" in r && i(14, w = r.elem_style), "$$scope" in r && i(19, _ = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    128 && b.update((r) => ({
      ...r,
      ...m
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, title*/
    294720 && R({
      gradio: a,
      props: c,
      _internal: f,
      visible: S,
      elem_id: K,
      elem_classes: I,
      elem_style: w,
      as_item: C,
      title: h
    }), e.$$.dirty & /*$slotKey, $mergedProps, $slots, $columnItems*/
    229377 && U(l, s._internal.index || 0, {
      props: {
        style: s.elem_style,
        className: $(s.elem_classes, "ms-gr-antd-table-column-group"),
        id: s.elem_id,
        title: s.title,
        ...s.props,
        ...X(s)
      },
      slots: o,
      children: n || []
    });
  }, [s, b, E, N, O, q, a, m, f, h, C, S, K, I, w, n, o, l, c, _, u];
}
class pt extends ot {
  constructor(t) {
    super(), mt(this, t, gt, ht, bt, {
      gradio: 6,
      props: 7,
      _internal: 8,
      title: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), d();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(t) {
    this.$$set({
      props: t
    }), d();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), d();
  }
  get title() {
    return this.$$.ctx[9];
  }
  set title(t) {
    this.$$set({
      title: t
    }), d();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), d();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), d();
  }
}
export {
  pt as default
};
