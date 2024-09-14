function X(e) {
  const {
    gradio: t,
    _internal: i,
    ...n
  } = e;
  return Object.keys(i).reduce((o, s) => {
    const r = s.match(/bind_(.+)_event/);
    if (r) {
      const c = r[1], u = c.split("_"), _ = (...m) => {
        const y = m.map((f) => m && typeof f == "object" && (f.nativeEvent || f instanceof Event) ? {
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
          payload: y,
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
        const y = u[u.length - 1];
        return m[`on${y.slice(0, 1).toUpperCase()}${y.slice(1)}`] = _, o;
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
function b(e, t = k) {
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
  function r(c, u = k) {
    const _ = [c, u];
    return n.add(_), n.size === 1 && (i = t(o, s) || k), c(e), () => {
      n.delete(_), n.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: s,
    subscribe: r
  };
}
const {
  getContext: F,
  setContext: P
} = window.__gradio__svelte__internal, L = "$$ms-gr-antd-slots-key";
function Z() {
  const e = b({});
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
  const n = F(B), o = ((c = g(n)) == null ? void 0 : c.as_item) || e.as_item, s = n ? o ? g(n)[o] : g(n) : {}, r = b({
    ...e,
    ...s
  });
  return n ? (n.subscribe((u) => {
    const {
      as_item: _
    } = g(r);
    _ && (u = u[_]), r.update((a) => ({
      ...a,
      ...u
    }));
  }), [r, (u) => {
    const _ = u.as_item ? g(n)[u.as_item] : g(n);
    return r.set({
      ...u,
      ..._
    });
  }]) : [r, (u) => {
    r.set(u);
  }];
}
const M = "$$ms-gr-antd-slot-key";
function H() {
  P(M, b(void 0));
}
function V() {
  return F(M);
}
const J = "$$ms-gr-antd-component-slot-context-key";
function Q({
  slot: e,
  index: t,
  subIndex: i
}) {
  return P(J, {
    slotKey: b(e),
    slotIndex: b(t),
    subSlotIndex: b(i)
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
      for (var s = "", r = 0; r < arguments.length; r++) {
        var c = arguments[r];
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
      var r = "";
      for (var c in s)
        t.call(s, c) && s[c] && (r = o(r, c));
      return r;
    }
    function o(s, r) {
      return r ? s ? s + " " + r : s + r : s;
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
    const s = o.reduce((r, c) => (r[c] = b([]), r), {});
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
    return function(r, c, u) {
      o && (r ? o[r].update((_) => {
        const a = [..._];
        return s.includes(r) ? a[c] = u : a[c] = void 0, a;
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
} = nt("tree"), {
  SvelteComponent: ot,
  check_outros: rt,
  component_subscribe: x,
  create_slot: lt,
  detach: ct,
  empty: ut,
  flush: d,
  get_all_dirty_from_scope: ft,
  get_slot_changes: _t,
  group_outros: at,
  init: mt,
  insert: dt,
  safe_not_equal: yt,
  transition_in: v,
  transition_out: j,
  update_slot_base: bt
} = window.__gradio__svelte__internal;
function A(e) {
  let t;
  const i = (
    /*#slots*/
    e[20].default
  ), n = lt(
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
      524288) && bt(
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
    e[0].visible && A(e)
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
      1 && v(n, 1)) : (n = A(o), n.c(), v(n, 1), n.m(t.parentNode, t)) : n && (at(), j(n, 1, 1, () => {
        n = null;
      }), rt());
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
  let n, o, s, r, c, {
    $$slots: u = {},
    $$scope: _
  } = t, {
    gradio: a
  } = t, {
    props: m = {}
  } = t;
  const y = b(m);
  x(e, y, (l) => i(18, c = l));
  let {
    _internal: f = {}
  } = t, {
    as_item: h
  } = t, {
    title: C
  } = t, {
    visible: K = !0
  } = t, {
    elem_id: S = ""
  } = t, {
    elem_classes: w = []
  } = t, {
    elem_style: I = {}
  } = t;
  const E = V();
  x(e, E, (l) => i(17, r = l));
  const [N, R] = G({
    gradio: a,
    props: c,
    _internal: f,
    visible: K,
    elem_id: S,
    elem_classes: w,
    elem_style: I,
    as_item: h,
    title: C
  });
  x(e, N, (l) => i(0, s = l));
  const O = Z();
  x(e, O, (l) => i(16, o = l));
  const U = it(), {
    default: q
  } = st();
  return x(e, q, (l) => i(15, n = l)), e.$$set = (l) => {
    "gradio" in l && i(6, a = l.gradio), "props" in l && i(7, m = l.props), "_internal" in l && i(8, f = l._internal), "as_item" in l && i(9, h = l.as_item), "title" in l && i(10, C = l.title), "visible" in l && i(11, K = l.visible), "elem_id" in l && i(12, S = l.elem_id), "elem_classes" in l && i(13, w = l.elem_classes), "elem_style" in l && i(14, I = l.elem_style), "$$scope" in l && i(19, _ = l.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    128 && y.update((l) => ({
      ...l,
      ...m
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, title*/
    294720 && R({
      gradio: a,
      props: c,
      _internal: f,
      visible: K,
      elem_id: S,
      elem_classes: w,
      elem_style: I,
      as_item: h,
      title: C
    }), e.$$.dirty & /*$slotKey, $mergedProps, $slots, $items*/
    229377 && U(r, s._internal.index || 0, {
      props: {
        style: s.elem_style,
        className: $(s.elem_classes, "ms-gr-antd-tree-node"),
        id: s.elem_id,
        title: s.title,
        ...s.props,
        ...X(s)
      },
      slots: o,
      children: n.length > 0 ? n : void 0
    });
  }, [s, y, E, N, O, q, a, m, f, h, C, K, S, w, I, n, o, r, c, _, u];
}
class pt extends ot {
  constructor(t) {
    super(), mt(this, t, gt, ht, yt, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      title: 10,
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
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), d();
  }
  get title() {
    return this.$$.ctx[10];
  }
  set title(t) {
    this.$$set({
      title: t
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
