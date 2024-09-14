function X(n) {
  const {
    gradio: t,
    _internal: i,
    ...e
  } = n;
  return Object.keys(i).reduce((o, s) => {
    const l = s.match(/bind_(.+)_event/);
    if (l) {
      const c = l[1], u = c.split("_"), a = (...m) => {
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
          component: e
        });
      };
      if (u.length > 1) {
        let m = {
          ...e.props[u[0]] || {}
        };
        o[u[0]] = m;
        for (let f = 1; f < u.length - 1; f++) {
          const h = {
            ...e.props[u[f]] || {}
          };
          m[u[f]] = h, m = h;
        }
        const b = u[u.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = a, o;
      }
      const _ = u[0];
      o[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = a;
    }
    return o;
  }, {});
}
function k() {
}
function Y(n, t) {
  return n != n ? t == t : n !== t || n && typeof n == "object" || typeof n == "function";
}
function D(n, ...t) {
  if (n == null) {
    for (const e of t)
      e(void 0);
    return k;
  }
  const i = n.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function p(n) {
  let t;
  return D(n, (i) => t = i)(), t;
}
const g = [];
function y(n, t = k) {
  let i;
  const e = /* @__PURE__ */ new Set();
  function o(c) {
    if (Y(n, c) && (n = c, i)) {
      const u = !g.length;
      for (const a of e)
        a[1](), g.push(a, n);
      if (u) {
        for (let a = 0; a < g.length; a += 2)
          g[a][0](g[a + 1]);
        g.length = 0;
      }
    }
  }
  function s(c) {
    o(c(n));
  }
  function l(c, u = k) {
    const a = [c, u];
    return e.add(a), e.size === 1 && (i = t(o, s) || k), c(n), () => {
      e.delete(a), e.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: s,
    subscribe: l
  };
}
const {
  getContext: F,
  setContext: P
} = window.__gradio__svelte__internal, L = "$$ms-gr-antd-slots-key";
function Z() {
  const n = y({});
  return P(L, n);
}
const B = "$$ms-gr-antd-context-key";
function G(n) {
  var c;
  if (!Reflect.has(n, "as_item") || !Reflect.has(n, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = V(), i = Q({
    slot: void 0,
    index: n._internal.index,
    subIndex: n._internal.subIndex
  });
  t && t.subscribe((u) => {
    i.slotKey.set(u);
  }), H();
  const e = F(B), o = ((c = p(e)) == null ? void 0 : c.as_item) || n.as_item, s = e ? o ? p(e)[o] : p(e) : {}, l = y({
    ...n,
    ...s
  });
  return e ? (e.subscribe((u) => {
    const {
      as_item: a
    } = p(l);
    a && (u = u[a]), l.update((_) => ({
      ..._,
      ...u
    }));
  }), [l, (u) => {
    const a = u.as_item ? p(e)[u.as_item] : p(e);
    return l.set({
      ...u,
      ...a
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
  return F(M);
}
const J = "$$ms-gr-antd-component-slot-context-key";
function Q({
  slot: n,
  index: t,
  subIndex: i
}) {
  return P(J, {
    slotKey: y(n),
    slotIndex: y(t),
    subSlotIndex: y(i)
  });
}
function T(n) {
  return n && n.__esModule && Object.prototype.hasOwnProperty.call(n, "default") ? n.default : n;
}
var z = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(n) {
  (function() {
    var t = {}.hasOwnProperty;
    function i() {
      for (var s = "", l = 0; l < arguments.length; l++) {
        var c = arguments[l];
        c && (s = o(s, e(c)));
      }
      return s;
    }
    function e(s) {
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
    n.exports ? (i.default = i, n.exports = i) : window.classNames = i;
  })();
})(z);
var W = z.exports;
const $ = /* @__PURE__ */ T(W), {
  getContext: tt,
  setContext: et
} = window.__gradio__svelte__internal;
function nt(n) {
  const t = `$$ms-gr-antd-${n}-context-key`;
  function i(o = ["default"]) {
    const s = o.reduce((l, c) => (l[c] = y([]), l), {});
    return et(t, {
      itemsMap: s,
      allowedSlots: o
    }), s;
  }
  function e() {
    const {
      itemsMap: o,
      allowedSlots: s
    } = tt(t);
    return function(l, c, u) {
      o && (l ? o[l].update((a) => {
        const _ = [...a];
        return s.includes(l) ? _[c] = u : _[c] = void 0, _;
      }) : s.includes("default") && o.default.update((a) => {
        const _ = [...a];
        return _[c] = u, _;
      }));
    };
  }
  return {
    getItems: i,
    getSetItemFn: e
  };
}
const {
  getItems: st,
  getSetItemFn: it
} = nt("menu"), {
  SvelteComponent: ot,
  check_outros: lt,
  component_subscribe: x,
  create_slot: rt,
  detach: ct,
  empty: ut,
  flush: d,
  get_all_dirty_from_scope: ft,
  get_slot_changes: at,
  group_outros: _t,
  init: mt,
  insert: dt,
  safe_not_equal: bt,
  transition_in: v,
  transition_out: j,
  update_slot_base: yt
} = window.__gradio__svelte__internal;
function A(n) {
  let t;
  const i = (
    /*#slots*/
    n[20].default
  ), e = rt(
    i,
    n,
    /*$$scope*/
    n[19],
    null
  );
  return {
    c() {
      e && e.c();
    },
    m(o, s) {
      e && e.m(o, s), t = !0;
    },
    p(o, s) {
      e && e.p && (!t || s & /*$$scope*/
      524288) && yt(
        e,
        i,
        o,
        /*$$scope*/
        o[19],
        t ? at(
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
      t || (v(e, o), t = !0);
    },
    o(o) {
      j(e, o), t = !1;
    },
    d(o) {
      e && e.d(o);
    }
  };
}
function ht(n) {
  let t, i, e = (
    /*$mergedProps*/
    n[0].visible && A(n)
  );
  return {
    c() {
      e && e.c(), t = ut();
    },
    m(o, s) {
      e && e.m(o, s), dt(o, t, s), i = !0;
    },
    p(o, [s]) {
      /*$mergedProps*/
      o[0].visible ? e ? (e.p(o, s), s & /*$mergedProps*/
      1 && v(e, 1)) : (e = A(o), e.c(), v(e, 1), e.m(t.parentNode, t)) : e && (_t(), j(e, 1, 1, () => {
        e = null;
      }), lt());
    },
    i(o) {
      i || (v(e), i = !0);
    },
    o(o) {
      j(e), i = !1;
    },
    d(o) {
      o && ct(t), e && e.d(o);
    }
  };
}
function pt(n, t, i) {
  let e, o, s, l, c, {
    $$slots: u = {},
    $$scope: a
  } = t, {
    gradio: _
  } = t, {
    props: m = {}
  } = t;
  const b = y(m);
  x(n, b, (r) => i(18, c = r));
  let {
    _internal: f = {}
  } = t, {
    as_item: h
  } = t, {
    label: C
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
  x(n, E, (r) => i(17, l = r));
  const [N, R] = G({
    gradio: _,
    props: c,
    _internal: f,
    visible: K,
    elem_id: S,
    elem_classes: w,
    elem_style: I,
    as_item: h,
    label: C
  });
  x(n, N, (r) => i(0, s = r));
  const O = Z();
  x(n, O, (r) => i(16, o = r));
  const U = it(), {
    default: q
  } = st();
  return x(n, q, (r) => i(15, e = r)), n.$$set = (r) => {
    "gradio" in r && i(6, _ = r.gradio), "props" in r && i(7, m = r.props), "_internal" in r && i(8, f = r._internal), "as_item" in r && i(9, h = r.as_item), "label" in r && i(10, C = r.label), "visible" in r && i(11, K = r.visible), "elem_id" in r && i(12, S = r.elem_id), "elem_classes" in r && i(13, w = r.elem_classes), "elem_style" in r && i(14, I = r.elem_style), "$$scope" in r && i(19, a = r.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*props*/
    128 && b.update((r) => ({
      ...r,
      ...m
    })), n.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, label*/
    294720 && R({
      gradio: _,
      props: c,
      _internal: f,
      visible: K,
      elem_id: S,
      elem_classes: w,
      elem_style: I,
      as_item: h,
      label: C
    }), n.$$.dirty & /*$slotKey, $mergedProps, $items, $slots*/
    229377 && U(l, s._internal.index || 0, {
      props: {
        style: s.elem_style,
        className: $(s.elem_classes, s.props.type ? `ms-gr-antd-menu-item-${s.props.type}` : "ms-gr-antd-menu-item", e.length > 0 ? "ms-gr-antd-menu-item-submenu" : ""),
        id: s.elem_id,
        label: s.label,
        ...s.props,
        ...X(s)
      },
      slots: o,
      children: e.length > 0 ? e : void 0
    });
  }, [s, b, E, N, O, q, _, m, f, h, C, K, S, w, I, e, o, l, c, a, u];
}
class gt extends ot {
  constructor(t) {
    super(), mt(this, t, pt, ht, bt, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      label: 10,
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
  get label() {
    return this.$$.ctx[10];
  }
  set label(t) {
    this.$$set({
      label: t
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
  gt as default
};
